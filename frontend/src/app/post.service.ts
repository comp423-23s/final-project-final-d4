import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError, from, async } from 'rxjs';
import { filter, first } from 'rxjs/operators';
import { map, mergeMap } from 'rxjs/operators';
import { Comment } from './comment';

export interface Post {
    id: number;
    content: string; 
    created: Date;
    postedBy: number;
    comments: Comment[];
    tags: string[];
}

// This class handles the post related concerns of the system 
// including getter and setter of posts
  @Injectable({
    providedIn: 'root'
  })
  export class PostService {
  
    constructor(private http: HttpClient) { }

    // get all posts from post system
    // returns obervable array of post object
    getPosts(): Observable<Post[]> {
      return this.http.get<Post[]>("/api/post");
    }

  }