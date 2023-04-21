import { Component } from '@angular/core';
import { PostView, PostsService } from '../post.service';
import { ActivatedRoute } from '@angular/router';
import { CommentService } from '../comment.service';
import { Comment } from '../comment.model';
import { newComment } from '../comment.service';
import { PermissionService } from '../permission.service';
import { Observable, catchError, throwError } from 'rxjs';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-post-details',
  templateUrl: './post-details.component.html',
  styleUrls: ['./post-details.component.css']
})
export class PostDetailsComponent {
  post!: PostView;
  comments: Comment[] = [];
  projectId!: number;
  selectedValue!: string;
  deleteAdminPermission$: Observable<Boolean>;

  constructor(
    private route: ActivatedRoute,
    private postService: PostsService,
    private commentService: CommentService,
    private permission: PermissionService) {
      this.deleteAdminPermission$ = this.permission.check('comment.delete', 'comment/')
    }

  ngOnInit(): void {
    const postId = Number(this.route.snapshot.paramMap.get('id'));
    this.postService.getPostById(postId).subscribe((post) => {
      this.post = post;
    });
    this.projectId = postId; 
    this.getComments();
  }

  getComments(): void {
    this.commentService.getComments(this.projectId).subscribe((comments) => {
      this.comments = comments;
    });
  }

  addComment(text: string, isPrivate: string): void {
    // this.commentService.addComment(text, this.post.id, isPrivate).subscribe((comment: Comment) => {
    //   this.comments.push(comment);
    // });
  }

  deleteComment(comment_id: number): void {
    this.commentService.deleteComment(this.projectId,comment_id)
    .pipe(
      catchError(this.onError)
    )
    .subscribe(() => {
      console.log("deleting from frontend");
      this.comments = this.comments.filter((comment) => comment.id !== comment_id);
    });
  }

  getDeleteUserPermission(commenter: number): Observable<boolean> {
    return this.permission.checkPID(commenter);
  }

  resetcomment():void {
    this.commentService.getComments(this.projectId).subscribe((comments) => {
      this.comments = comments;
    });
  }

  private onError(err: HttpErrorResponse) {
    if (err.message) {
      window.alert(err.error.detail);
    } else {
      window.alert("Unknown error: " + JSON.stringify(err));
    }
    return throwError(err);
  }
}
