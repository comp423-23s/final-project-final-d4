import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import { PostsService } from '../post.service';
import { Post } from '../post.service';


@Component({
  selector: 'app-post-list',
  templateUrl: './post-list.component.html',
  styleUrls: ['./post-list.component.css']
})
export class PostListComponent {
  
  public posts: Observable<Post[]>;

  constructor(public postService: PostsService){
    this.posts = postService.getPost()

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
