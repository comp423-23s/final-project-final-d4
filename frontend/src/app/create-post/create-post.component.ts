import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Post, PostsService } from '../post.service';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-create-post',
  templateUrl: './create-post.component.html',
  styleUrls: ['./create-post.component.css']
})
export class CreatePostComponent {

  constructor(
    public postService: PostsService
  ) {}


  onPost(form: NgForm):void{
    let postedBy = parseInt(form.value.postedBy ?? "");
    let title = (form.value.title ?? "");
    let description = (form.value.description ?? "");
    let content = (form.value.content ?? "");
    let created = (form.value.created);
    let comments = (form.value.comments ?? "");
    let tags = (form.value.tags ?? "");
    // this.postService.addPost(form.value.id, form.value.title, form.value.descripiton, form.value.content, form.value.dateTime, form.value.tag);
    // 

    this.postService
      .addPost( title, description, content, created, postedBy, comments, tags)
      .subscribe({
        next: (post) => this.onSuccess(post),
        error:(err) => this.onError(err)
      });
    
    form.resetForm()
  }

  private onSuccess(post: Post): void {
    window.alert(`Thanks for posting`);
  }

  private onError(err: HttpErrorResponse) {
    if (err.message) {
      window.alert(err.error.detail);
    } else {
      window.alert("Unknown error: " + JSON.stringify(err));
    }
  }


}
