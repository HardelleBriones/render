from fastapi import status, HTTPException, Response, APIRouter, Depends
from authentication import oauth2
from services.knowledge_base_services import (
    delete_file, 
    get_all_files,
    get_all_course,
    delete_course_file,
    )
from services.memory_services import ChatHistory
from services.facebook_services import get_facebook_page_posts
from data_definitions.schemas import Facebook_data
router = APIRouter(
    prefix="/knowledge_base",
    tags=["knowledge_base"]
)    

@router.get("/get_facebook_data")
def get_facebook_data():
    try:
        posts = get_facebook_page_posts()
        if posts:
            facebook_data_list = []
            for post in posts['data']:
                facebook_data = Facebook_data(
                    post_id=post.get('id'),
                    created_time=post.get('created_time'),
                    content=post.get('message')
                )
                facebook_data_list.append(facebook_data)
            return facebook_data_list
        else:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No facebook data found") 
                
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) 
    
@router.get("/get_files")
def get_all_filenames():
    try:
        courses = get_all_course()
        result = {}
        for course in courses:
            files = get_all_files(course)
            result[course] = files
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) 


@router.get("/get_files_by_course/")
def get_course_files(course_name:str):
    try:
        result = get_all_files(course_name)
        if result:
            return result
        else:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No files or course found")
    except ValueError as e:
        # Raise an HTTPException with status code 404 (Not Found) if the course is not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) 

@router.get("/get_course/")
def get_course():
    #current_user: str = Depends(oauth2.get_current_user)
    try:
   
        result = get_all_course()
        if result:
            return result
        else:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        # Raise an HTTPException with status code 404 (Not Found) if the course is not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) 
    
@router.delete("/{file_name_to_delete}/")
def delete_course_files(course_name: str, file_name_to_delete: str):  
    try:
        if not course_name in get_all_course():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{course_name} not found")

        if file_name_to_delete in get_all_files(course_name):
            delete_file(course_name,file_name_to_delete)
            delete_course_file(course_name,file_name_to_delete)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{file_name_to_delete} not found")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        # Raise an HTTPException with status code 404 (Not Found) if the course is not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) 
   

















    