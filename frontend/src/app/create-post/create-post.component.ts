import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Post, PostsService } from '../post.service';

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

    let postedBy = parseInt(form.value.id ?? "");
    let title = (form.value.title ?? "");
    let description = (form.value.description ?? "");
    let content = (form.value.content ?? "");
    let time = (form.value.dateTime)
    let tag = (form.value.tag ?? "");
    // this.postService.addPost(form.value.id, form.value.title, form.value.descripiton, form.value.content, form.value.dateTime, form.value.tag);
    // 

    this.postService
      .addPost(postedBy, title, content, description, time, tag)
      .subscribe({
        next: (post) => this.onSuccess(post),
        error:(err) => this.onError(err)
      });
    
    form.resetForm()
  }

  private onSuccess(post: Post): void {
    window.alert(`Thanks for posting`);
  }

  private onError(err: Error) {
    if (err.message) {
      window.alert(err.message);
    } else {
      window.alert("Unknown error: " + JSON.stringify(err));
    }
  }


}
