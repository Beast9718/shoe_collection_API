from fastapi import APIRouter,Depends,status,BackgroundTasks
from .schemas import UserCreateModel,UserModel,UserLoginModel,UserShoesModel,EmailModel,PasswordResetConfirmModel,PasswordResetRequestModel
from .service import UserService
from src.db.main import get_session 
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from .utils import create_access_token,decode_token,verify_password,create_url_safe_token,decode_url_safe_token,generate_password_hash
from datetime import timedelta,datetime
from fastapi.responses import JSONResponse
from .dependencies import RefreshTokenBearer,AccessTokenBearer,get_current_user,RoleChecker
from src.db.redis import add_jti_to_blocklist
# from src.mail import mail,create_message
from src.mail import send_email
from src.config import Config
# from src.celery_tasks import send_email


auth_router=APIRouter()
user_service=UserService()
REFRESH_EXPIRY_TOKEN=2
role_checker=Depends(RoleChecker(["admin","user"]))

    

@auth_router.post(
        '/signup',
        # response_model=UserModel,
        status_code=status.HTTP_201_CREATED
        
        )
async def create_user_Account(user_data:UserCreateModel,bg_tasks:BackgroundTasks,session:AsyncSession=Depends(get_session)):
    email=user_data.email

    user_exists=await user_service.user_exists(email,session)

    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="user with email already exist")
    
    new_user=await user_service.create_user(user_data,session)
    
    token=create_url_safe_token({"email":email})
    link=f"https://{Config.Domain}/api/v1/auth/verify/{token}"

    html=f"""
    <h1>Verify your email</h1>
    <p>please click this <a href="{link}">link</a> to verify your mail
    """
    subject="verify your email"
    # message=create_message(recipients=[email],subject=subject,body=html)
    # bg_tasks.add_task(mail.send_message,message)
    # send_email.delay([email],subject,html)
    bg_tasks.add_task(send_email,[email],subject,html)
    # send_email([email],subject,html)
    return{
        "message":"Account create! Check mail to verify account",
        "user":new_user,
    }

@auth_router.post('/login')
async def login_user(login_data:UserLoginModel,session:AsyncSession=Depends(get_session)):
    email=login_data.email
    password=login_data.password

    user=await user_service.get_user_by_email(email,session)
    if user is not None:
        password_valid=verify_password(password,user.password_hash)

        if password_valid:
            access_token=create_access_token(
                user_data={
                    'email':user.email,
                    'user_uid':str(user.uid),
                    'role':user.role
                },
                
            )

            refresh_token=create_access_token(
                user_data={
                    'email':user.email,
                    'user_uid':str(user.uid)
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_EXPIRY_TOKEN)
            )

            return JSONResponse(
                content={
                    "message":"login successful",
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    "user":{
                        "email":user.email,
                        "uid":str(user.uid)
                    }
                }
            )
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Invalid Email or Password'
    )
        
@auth_router.get('/refresh_token')
async def get_new_access_token(token_details:dict=Depends(RefreshTokenBearer())):
    expiry_timestamp=token_details["exp"]
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token=create_access_token(user_data=token_details["user"])

        return JSONResponse(content={
            "access_token":new_access_token
        })
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid or Expired token")

@auth_router.get('/me',response_model=UserShoesModel,dependencies=[role_checker])
async def get_current_user(user=Depends(get_current_user)):
    return user

@auth_router.get('/logout')
async def revoke_token(token_details:dict=Depends(AccessTokenBearer())):
    jti=token_details['jti']
    await add_jti_to_blocklist(jti)
    return JSONResponse(
        content={
            "message":"Logged Out Successfully"
        },
        status_code=status.HTTP_200_OK
    )

@auth_router.post('/send_mail')
async def send_mail(emails:EmailModel,bg_tasks:BackgroundTasks):
    emails=emails.addresses
    subject="Welcome to our app"
    html="<h1>Welcome to the app</h1>"
    # message=create_message(recipients=emails,subject=subject,body=html)
    # bg_tasks.add_task(mail.send_message,message)
    # send_email.delay(emails,subject,html)
    bg_tasks.add_task(send_email,emails,subject,html)
    # send_email(emails,subject,html)
    return{"message":"Email sent successfully"}


@auth_router.get("/verify/{token}")
async def verify_user_account(token:str,session:AsyncSession=Depends(get_session)):
    token_data=decode_url_safe_token(token)
    if not token_data:
        raise HTTPException(
            status_code=400,
            detail="invalid or expired token"
        )

    user_email=token_data.get('email')

    if user_email:
        user=await user_service.get_user_by_email(user_email,session)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
        await user_service.update_user(user,{"is_verified":True},session)

        return JSONResponse(
            content={
                "message":"Account verified successfully"},
                status_code=status.HTTP_200_OK,
        )
    return JSONResponse(
        content={
            "message":"ERROR occured during verification"
        },
        status_code=status.HTTP_400_BAD_REQUEST,
    )
    
    

@auth_router.post("/password-reset-request")
async def password_reset_request(email_data:PasswordResetRequestModel,bg_tasks:BackgroundTasks):
    email=email_data.email

    token=create_url_safe_token({"email":email})
    link=f"https://{Config.Domain}/api/v1/auth/password-reset-confirm/{token}"

    html=f"""
    <h1>Reset your Password</h1>
    <p>please click this <a href="{link}">link</a> to Reset your Password
    """
    recipients=[email]
    subject="Reset your Password"
    # message=create_message(recipients=recipients,subject=subject,body=html_message)
    # bg_tasks.add_task(mail.send_message,message)
    # send_email.delay(recipients,subject,html_message)
    bg_tasks.add_task(send_email,recipients,subject,html)
    # send_email(recipients,subject,html)
    return JSONResponse(
        content={
            "message":"please check your email for instructions to reset your password"
        },
        status_code=status.HTTP_200_OK
    )

@auth_router.post("/password-reset-confirm/{token}")
async def reset_account_password(token:str,passwords:PasswordResetConfirmModel,session:AsyncSession=Depends(get_session)):
    new_password=passwords.new_password
    confirm_password=passwords.confirm_new_password
    if new_password!=confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="password do not match")
    
    
    token_data=decode_url_safe_token(token)
    if not token_data:
        raise HTTPException(
            status_code=400,
            detail="invalid or expired token"
        )
    
    user_email=token_data.get('email')

    if user_email:
        user=await user_service.get_user_by_email(user_email,session)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
        password_hash=generate_password_hash(new_password)
        await user_service.update_user(user,{"password_hash":password_hash},session)

        return JSONResponse(
            content={
                "message":"Password reset successfully"},
                status_code=status.HTTP_200_OK,
        )
    return JSONResponse(
        content={
            "message":"ERROR occured during password reset"
        },
        status_code=status.HTTP_400_BAD_REQUEST,
    )
    