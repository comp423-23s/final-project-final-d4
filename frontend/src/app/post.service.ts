import { Injectable } from "@angular/core";
import { Observable, throwError } from "rxjs";
import { HttpClient } from "@angular/common/http";
import {ProfileService, Profile} from "./profile/profile.service"

export interface Post{
    title: string;
    description: string;
    content: string;
    created: Date;
    postedBy: number;
    comments: string[];
    tags: string[];
}

export interface PostView {
    id: number;
    content: string;
    tags: string[]
    created: Date;
    title: string;
    description: string;
    pid: number;
    // first_name: string;
    // last_name: string;
}

// FYI:
//  Backend Post Model
// class Post(BaseModel):
//     # this is the primary key
//     id: int | None = None
//     content: str=""
//     tags: list[str] = []
//     created: datetime = datetime.now()
//     title: str = ""
//     description: str = ""

// Backend NewPost (PostRequest) Model:
// class Post(BaseModel):
//     content: str=""
//     tags: list[str] = []
//     created: datetime = datetime.now()
//     title: str = ""
//     description: str = ""


@Injectable({providedIn: 'root'})
export class PostsService{
    private profile$: Observable<Profile | undefined>;
    constructor(
        private http: HttpClient, 
        private profileService: ProfileService) {
            this.profile$ = profileService.profile$
        }

    //Retrieve all posts in the list .
    // @returns observable array of Post objects.

    getPost(): Observable<PostView[]> {
        return this.http.get<PostView[]>("/api/post");
    }

    /**
   * create a post
   * 
   * @param id: username number
   * @param title: title of the post 
   * @param description: description of the post 
   * @param dateTime: time when the post is made
   * @param tag: tag of the post
   * @returns Obervable of Post that will error if there are issues with validation or persistence.
   */
    addPost(title: string, description: string, content: string,  created: any, postedBy: number, comments: string[], tags: string[]){
        //make sure users fill in each input 

        let errors: string[] = [];

        if(postedBy.toString().length !== 9){
            errors.push(`Username required.`);
        }
        if(title === ""){
            errors.push(`Title required.`);
        }
        if(description === ""){
            errors.push(`Description required.`);
        }
        if(content === ""){
            errors.push(`Content required.`);
        }

        if (errors.length > 0) {
            return throwError(() => { return new Error(errors.join("\n")) });
        }

        //create post with the parameters
        let post: Post = {title: title, description: description, content: content,  created: new Date(), postedBy: postedBy, comments: comments, tags: tags};

        //return post
        return this.http.post<Post>("/api/post", post);
        
    }

    deletePost(postID: number): Observable<Post> {
        return this.http.delete<Post>(`/api/post/${postID}`)
    }
}