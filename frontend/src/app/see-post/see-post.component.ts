import { Component } from '@angular/core';
import {PostService,Post} from '../post.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-see-post',
  templateUrl: './see-post.component.html',
  styleUrls: ['./see-post.component.css']
})
export class SeePostComponent {

  public posts$ : Observable<Post[]>;
  
  constructor(private postService: PostService){
    this.posts$ = postService.getPosts()
  }
}
