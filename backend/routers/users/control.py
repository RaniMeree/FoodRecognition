from fastapi import APIRouter,Depends ,HTTPException ,status, Response, Query
from depends_functions import *
from sqlalchemy.orm import Session
from .schema import *
from database import models
import bcrypt 
from binascii import unhexlify 
from settings import *
from math import floor  # Import for calorie calculation
router = APIRouter(
    prefix="/api/users",
)



@router.post("/authentication/signup", status_code=status.HTTP_201_CREATED,  tags = [Tags.users])
async def create_user(user: CreateUser,
                      db: Session = Depends(get_db),
                      ) :
    
    token = generate_token(length=30)
    
    

    print(user.dict())
    new_user = models.Users(**user.dict(), token=token, role='user')
    hash_password = bcrypt.hashpw(new_user.password.encode('utf-8'), bcrypt.gensalt())
    new_user.password = hash_password
    age = user.age
    weight = user.weight
    height = user.height / 100
    try:
        if user.gender == "Male":
            bmr = 10 * weight + 6.25 * height * 100 - 5 * age + 5  # Convert cm to m for calculation
        else:
            bmr = 10 * weight + 6.25 * height * 100 - 5 * age - 161  # Convert cm to m for calculation

        # Calculate activity factor based on user selection
        activity_factor = {
            "No Exercise": 1.2,
            "Once a week": 1.4,
            "2-3 times per week": 1.6,
            "4-5 times per week": 1.9,
        }[user.activity]

        # Calculate required calories
        required_calories = floor(bmr * activity_factor)

        new_user.requiredCalories = required_calories  # Add calculated calories to user object
        
        # Print the calculated required calories
        print(f"Calculated required calories for user {user.username}: {required_calories}")

        commitData(new_user, db)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username is already exists"
        )

    return {'token': token, 'username': new_user.username, 'requiredCalories': new_user.requiredCalories}

def authenticate_user(login_data: Login, db:Session = Depends(get_db)):
    user = check_user(login_data.email, db)
    print(user)
    if user and bcrypt.checkpw(login_data.password.encode('utf-8'),
                                user.password):
        
        return user
    raise  HTTPException(status_code = status.HTTP_409_CONFLICT,
                        detail=f"Incorrect username or password")

@router.post("/authentication/login",status_code = status.HTTP_200_OK, tags = [Tags.users])
async def login(response: Response,
                user = Depends(authenticate_user)
                ) -> AuthRespose :
    return user


@router.get("", status_code = status.HTTP_200_OK, tags = [Tags.users])
async def getUsers(page: int = Query(1, ge=1),
                    db:Session = Depends(get_db),
                    user: models.Users = Depends(auth_authz(permission=['super_admin'])),
                    ) -> ListUsers:

    users = db.query(models.Users).filter(models.Users.role == 'user')
    users_data = users.offset((page-1)*12).limit(12).all()
    users_count = users.count()
    return {"count": users_count, "users": users_data}

@router.get("/profile", status_code = status.HTTP_200_OK, tags = [Tags.users]) 
async def profile(checkUser: models.Users = Depends(auth_authz(permission = ['all'])),
                  db:Session = Depends(get_db)
                  ) -> UserInfo:
    return checkUser