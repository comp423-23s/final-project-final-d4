import { Component } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { PostsService } from '../post.service';
import { PostView } from '../post.service';
import { PermissionService } from '../permission.service';
import { Profile, ProfileService } from '../profile/profile.service';
import { HttpErrorResponse } from '@angular/common/http';
import { MatDialog } from '@angular/material/dialog';
import { NoSearchResultComponent } from '../no-search-result/no-search-result.component';
import { NoSearchStringComponent } from '../no-search-string/no-search-string.component';


@Component({
  selector: 'app-post-list',
  templateUrl: './post-list.component.html',
  styleUrls: ['./post-list.component.css']
})
export class PostListComponent {

  //declare search as string and initialize it as " "
  public search: string = "";
  
  // declares a public property posts that holds an observable of either a PostView[]
  public posts: Observable<PostView[]>;
  public deleteAdminPermission$: Observable<Boolean>;
  
  constructor(
    public postService: PostsService,
    private permission: PermissionService,
    public dialog: MatDialog,
    ){
    this.posts = postService.getPost()
    this.deleteAdminPermission$ = this.permission.check('delete.post', 'post/')
  }

  getDeleteUserPermission(postPID: number): Observable<boolean> {
    return this.permission.checkPID(postPID);
  }

  //search post from user input
  searchPost(search: string): void {
    if (search === ""){
      this.dialog.open(NoSearchStringComponent);
    } else {
      this.posts = this.postService.searchPost(search);
      this.posts.subscribe({
      next: (results: PostView[]) => {
        if (results.length === 0) {
          this.dialog.open(NoSearchResultComponent);
          this.posts = this.postService.getPost()
        } 
      },
      error: (err) => this.searchError(err)
      })
    }
    
  }

  private searchError(err: HttpErrorResponse): void{
    if (err.message) {
      window.alert(err.error.detail);
    } else {
      window.alert("Unknown error: " + JSON.stringify(err));
    }
  }

//reset the post list after search 
  resetSearch():void {
    this.posts = this.postService.getPost();
  }
  
  //delete post from project list
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

  addComment(){}

  private onError(err: HttpErrorResponse) {
    if (err.message) {
      window.alert(err.error.detail);
    } else {
      window.alert("Unknown error: " + JSON.stringify(err));
    }
    return throwError(err);
  }
  
  addPrivateComment(){
    
  }

}
