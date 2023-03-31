import { Injectable } from "@angular/core";

import { HttpClient } from "@angular/common/http";
import { Observable, throwError } from "rxjs";

export interface Post{
    postedBy: number;
    title: string;
    description: string;
    content: string;
    dateTime: Date;
    tag: string[];
    comment: string[];
}


@Injectable({providedIn: 'root'})
export class PostsService{
    constructor(private http: HttpClient) {}

    //Retrieve all posts in the list .
    // @returns observable array of Post objects.

    getPost(): Observable<Post[]> {
        return this.http.get<Post[]>("/api/post");
    }

    /**
   * create a post
   * 
   * @param id: username number
   * @param title: title of the post 
   * @param description: description of the post 
   * @param dateTime: time when the post is made
   * @param tag: tag of the post
   * @param comment: comment by other users 
   * @returns Obervable of Post that will error if there are issues with validation or persistence.
   */
    addPost(postedBy: number, title: string,  description: string, content: string,  dateTime: any, tag: string[], comment: string[]){
        //make sure users fill in each input 

        let errors: string[] = [];

        if(postedBy.toString() === ""){
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
        let post: Post = {postedBy: postedBy, title: title,  description: description, content: content, dateTime: new Date(), tag: tag, comment: comment};

        //return post
        return this.http.post<Post>("/api/post", post);
        
    }
}