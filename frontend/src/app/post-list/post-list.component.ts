import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import { PostsService } from '../post.service';
import { PostView } from '../post.service';


@Component({
  selector: 'app-post-list',
  templateUrl: './post-list.component.html',
  styleUrls: ['./post-list.component.css']
})
export class PostListComponent {

  search: string = " ";
  
  public posts: Observable<PostView[]>;

  constructor(public postService: PostsService){
    this.posts = postService.getPost()

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
  
  deletePost(postId: number) {
    // Call a service method to delete the post with the given ID
    this.postService.deletePost(postId).subscribe(() => {
      // Refresh the post list after successful deletion
      this.posts = this.postService.getPost();
    });
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
