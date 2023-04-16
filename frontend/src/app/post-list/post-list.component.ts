import { Component } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { PostsService } from '../post.service';
import { PostView } from '../post.service';
import { PermissionService } from '../permission.service';
import { Profile, ProfileService } from '../profile/profile.service';
import { HttpErrorResponse } from '@angular/common/http';


@Component({
  selector: 'app-post-list',
  templateUrl: './post-list.component.html',
  styleUrls: ['./post-list.component.css']
})
export class PostListComponent {

  // declare search as string and initialize as " "
  search: string = " ";
  
  // declares a public property posts that holds an observable of PostView[]
  public posts: Observable<PostView[]>;
  public deleteAdminPermission$: Observable<Boolean>;

  constructor(
    public postService: PostsService,
    private permission: PermissionService,
    ){
    this.posts = postService.getPost()
    this.deleteAdminPermission$ = this.permission.check('delete.post', 'post/')
  }

  getDeleteUserPermission(postPID: number): Observable<boolean> {
    return this.permission.checkPID(postPID);
  }

  //search post from user input
  searchPost(search: string): void {
    this.postService.searchPost(search).subscribe(() => {
      this.posts = this.postService.searchPost(search);
    });
  }

//reset the post list after search 
  resetSearch():void {
    this.postService.getPost().subscribe(() => {
      this.posts = this.postService.getPost();
    });
  }
  
  //deletePost from the post list
  deletePost(postId: number) {
    // Call a service method to delete the post with the given ID
    this.postService.deletePost(postId)
    .pipe(
      catchError(this.onError)
    )
    .subscribe(() => {
      // Refresh the post list after successful deletion
      this.posts = this.postService.getPost();
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



  // private onSuccess(): void {
  //   console.log("success")
  //   this.posts = this.postService.getPost()
  // }

  // private onError(err: Error) {
  //   if (err.message) {
  //     window.alert(err.message);
  //   } else {
  //     window.alert("Unknown error: " + JSON.stringify(err));
  //   }
  // }

}
