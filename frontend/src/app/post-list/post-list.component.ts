import { Component } from '@angular/core';
import { PostsService } from '../post.service';
import { Post } from './post.module';


@Component({
  selector: 'app-post-list',
  templateUrl: './post-list.component.html',
  styleUrls: ['./post-list.component.css']
})
export class PostListComponent {
  
  constructor(public postService: PostsService){

  }

  posts: Post[] = [];
 

  ngOnInit(){
    this.posts = this.postService.getPost();
  }

}
