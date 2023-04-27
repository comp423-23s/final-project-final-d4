import { Component } from '@angular/core';
import { PostView, PostsService } from '../post.service';
import { ActivatedRoute } from '@angular/router';
import { CommentService } from '../comment.service';
import { Comment } from '../comment.model';
import { newComment } from '../comment.service';
import { PermissionService } from '../permission.service';
import { Observable, catchError, throwError, map, shareReplay } from 'rxjs';
import { HttpErrorResponse } from '@angular/common/http';
import { Profile } from '../profile/profile.service';
import { MatDialog } from '@angular/material/dialog';
import { PostEditDialogComponent, UpdatedPost } from '../post-edit-dialog/post-edit-dialog.component';

@Component({
  selector: 'app-post-details',
  templateUrl: './post-details.component.html',
  styleUrls: ['./post-details.component.css']
})
export class PostDetailsComponent {
  post!: PostView;
  user!: Profile;
  comments: Comment[] = [];
  projectId!: number;
  selectedValue!: string;
  deleteAdminPermission$: Observable<Boolean>;
  editAdminPermission$: Observable<Boolean>;
  

  constructor(
    private route: ActivatedRoute,
    private postService: PostsService,
    private commentService: CommentService,
    private permission: PermissionService,
    public dialog: MatDialog) {
      this.deleteAdminPermission$ = this.permission.check('comment.delete', 'comment/')
      this.editAdminPermission$ = this.permission.check('edit.post', 'post/')
    }

  ngOnInit(): void {
    const postId = Number(this.route.snapshot.paramMap.get('id'));
    this.postService.getPostById(postId).subscribe((post) => {
      this.post = post;
      this.postService.getUserInfo(this.post.pid).subscribe((user) => {this.user = user;});
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
    this.commentService.addComment(text, this.post.id, isPrivate).subscribe((comment: Comment) => {
      this.comments.push(comment);
    });
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
  getEditUserPermission(postId: number): Observable<boolean> {
    return this.permission.checkPID(postId);
  }

  editPost(postId: number): void {
    
  }
  // editPost(postId: number): void {
  //   const dialogRef = this.dialog.open(PostEditDialogComponent, {
  //     width: '90%',
  //     height: '90%',
  //     data: {
  //       title: this.post.title,
  //       description: this.post.description,
  //       content: this.post.content,
  //       tags: this.post.tags,
  //     },
  //   });
  
  //   dialogRef.afterClosed().subscribe((result: UpdatedPost | undefined) => {
  //     if (result) {
  //       this.postService.updatePost(
  //           result.id,
  //           result.content,
  //           result.title,
  //           result.description,
  //           result.tags
  //         )
  //         .subscribe((updatedPost) => {
  //           this.post = updatedPost;
  //         });
  //     }
  //   });
  // }

  

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

  private userCache: { [key: string]: Observable<string> } = {};

  getUserFullName(comment: Comment): Observable<string> {
    const cachedValue = this.userCache[comment.commenter];
    if (cachedValue) {
      return cachedValue;
    }
    const newValue = this.postService.getUserInfo(comment.commenter).pipe(
      map(user => user ? `${user.first_name} ${user.last_name}` : ''),
      shareReplay(1) // cache the result
    );
    this.userCache[comment.commenter] = newValue;
    return newValue;
  }


}
