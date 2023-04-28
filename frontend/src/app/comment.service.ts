// comment.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map, throwError } from 'rxjs';
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
  let original_comment$: Observable<Comment[]> = this.http.get<Comment[]>(`/api/comment/${projectId}`);
  let new_comments = original_comment$.pipe(
    map((comments: Comment[]) => {
      return comments.map((comment: Comment) => {
        return {
          ...comment,
          created: new Date(comment.created)
        };
      }).sort((a, b) => {
        return b.created.getTime() - a.created.getTime();
      });
    })
  );
  return new_comments;
}


  addComment(text: string, postId: number, isPrivate: string): Observable<Comment> {
    if (!text) {
      return throwError(() => new Error('Content required'));
    }
    if (isPrivate === null) {
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