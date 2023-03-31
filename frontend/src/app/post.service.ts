import { Injectable } from "@angular/core";
import { Post } from "./post-list/post.module";


@Injectable({providedIn: 'root'})
export class PostsService{
    private posts: Post[] = [];

    addPost(id: number, title: string, description: string, content: string, dateTime: any, tag: string[]){
        const post: Post = {id: id,title: title, description: description, content: content, dateTime: new Date(), tag: tag};
        this.posts.push(post);
        
    }
    
    getPost(){
        return this.posts
    }
}