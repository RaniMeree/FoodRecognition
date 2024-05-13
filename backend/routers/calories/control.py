from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from depends_functions import *
from .schema import *
from database import models
import shutil
from ultralytics import YOLO

router = APIRouter(
    prefix="/api/calories",
)


def yolo_model(image):

    model = YOLO(f"{primary_path}/best.pt")
    results = model.predict(source=image, conf=0.25)

    food = ''
    for result in results:
        for detection in result.boxes:
            class_id = int(detection.cls)
            label = model.names[class_id]  
            food = label
            break
    return food
    
@router.post("/food-photo")
async def food_photo(file: UploadFile = File(...),
                     db: Session = Depends(get_db),
                     user: models.Users = Depends(auth_authz(permission=['all']))):
    file_extension = file.filename.split('.')[-1]
    image_name = generate_random_media_name(length=10, extension=file_extension)
    
    image_path = os.path.join(primary_path, image_name)
    
    try:
        with open(image_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        print(f"Error saving image: {e}")
        raise HTTPException(status_code=500, detail="Failed to save the image.")
    
    food = yolo_model(image_path)
    os.remove(image_path)
    
    if not food:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="The type of meal is not recognized, please send a clearer picture")
    
    food = db.query(models.Foods).filter(models.Foods.name == food).first()
    
    if food:
        return food
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This type of meal is not registered in the system")

    

@router.post("/calculation")
async def calculation(data: Calculation, 
                    db:Session = Depends(get_db),
                    user: models.Users = Depends(auth_authz(permission=['all']))
                    ):
    
    intake = models.Intake(
                    user_id=user.id,
                    foods_id=data.food_id,
                    count=data.intake_count,
                    )
    commitData(intake, db)
    return intake
 
@router.get("/intake")
async def intake(db:Session = Depends(get_db),
                user: models.Users = Depends(auth_authz(permission=['all']))
                ) -> list[IntakeRes]:
    
    data = user.intake
    return data