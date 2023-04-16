// comment.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Comment } from './comment.model';

export interface newComment {
    post: number;
    text: string;
    created: Date;
    isPrivate: boolean;
}

@Injectable({
  providedIn: 'root',
})
export class CommentService {
  
  constructor(private http: HttpClient) {}

  getComments(projectId: number): Observable<Comment[]> {
    return this.http.get<Comment[]>(`/api/comment/${projectId}`);
  }

  addComment(text: string, postId: number, isPrivate: boolean): Observable<Comment> {
    const comment: newComment = {
        post: postId,
        text,
        created: new Date(),
        isPrivate:isPrivate
      };

    return this.http.post<Comment>(`/api/comment`, comment);
  }

  deleteComment(id: number): Observable<void> {
    return this.http.delete<void>(`/api/comment/${id}`);
  }

}