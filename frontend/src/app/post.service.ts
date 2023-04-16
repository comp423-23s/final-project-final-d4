import { Injectable } from "@angular/core";
import { Observable, catchError, map, throwError } from "rxjs";
import { HttpClient, HttpErrorResponse } from "@angular/common/http";
import {ProfileService, Profile} from "./profile/profile.service"


export interface NewPost {
    content: string;
    tags: string[]
    created: Date;
    title: string;
    description: string;
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
   
    addPost(
      title: string, 
      description: string, 
      content: string, 
      tags: string[]) 
      {
        // Validate input
        if (!title) {
          return throwError(() => new Error('Title required'));
        }
        if (!description) {
          return throwError(() => new Error('Description required'));
        }
        if (!content) {
          return throwError(() => new Error('Content required'));
        }
      
        // Create post with the parameters
        const post: NewPost = {
          content,
          tags,
          created: new Date(),
          title,
          description,
        };
        
        return this.http.post<PostView>('/api/post', post);
      }

    getPostById(postId: number): Observable<PostView> {
        return this.http.get<PostView[]>(`/api/post`).pipe(
          map((posts) => posts.find((post) => post.id === postId) as PostView)
      );
    }

    deletePost(postID: number): Observable<PostView> {
        return this.http.delete<PostView>(`/api/post/${postID}`)
    }

    searchPost(searchText: string): Observable<PostView[]> {
        return this.http.get<PostView[]>(`/api/post/${searchText}`);
    }

  
}