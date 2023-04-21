// comment.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { Comment } from './comment.model';

export interface newComment {
    text: string;
    created: Date;
    private: boolean;
}

@Injectable({
  providedIn: 'root',
})
export class CommentService {
  
  constructor(private http: HttpClient) {}

  getComments(projectId: number): Observable<Comment[]> {
    return this.http.get<Comment[]>(`/api/comment/${projectId}`);
  }


  addComment(text: string, postId: number, isPrivate: string): Observable<Comment> {
    if (!text) {
      return throwError(() => new Error('Content required'));
    }
    if (!isPrivate) {
      return throwError(() => new Error('Status required'));
    }
    const comment: newComment = {
        text: text,
        created: new Date(),
        private: isPrivate === 'true'
      };
      return this.http.post<Comment>(`/api/comment/${postId}`, comment);
  }

  deleteComment(post_id: number, comment_id: number): Observable<void> {
    return this.http.delete<void>(`/api/comment/${post_id}/${comment_id}`);
  }

}