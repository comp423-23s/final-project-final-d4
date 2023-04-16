import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import { PostsService } from '../post.service';
import { Post, PostView } from '../post.service';


@Component({
  selector: 'app-post-list',
  templateUrl: './post-list.component.html',
  styleUrls: ['./post-list.component.css']
})
export class PostListComponent {

  //declare search as string and initialize it as " "
  search: string = " ";
  
  // declares a public property posts that holds an observable of either a PostView[]
  public posts: Observable<PostView[]>;

  constructor(public postService: PostsService){
    //Assigns the posts observable from the PostsService to the component's posts property.
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

  //delete the project from post list 
  deletePost(postId: number) {
    // Call a service method to delete the post with the given ID
    this.postService.deletePost(postId).subscribe(() => {
      // Refresh the post list after successful deletion
      this.posts = this.postService.getPost();
    });
  }


}
