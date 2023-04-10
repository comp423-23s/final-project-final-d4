import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Post, PostsService } from '../post.service';
import { Observable, Subscription } from 'rxjs';
import { ProfileService, Profile } from '../profile/profile.service';

@Component({
  selector: 'app-create-post',
  templateUrl: './create-post.component.html',
  styleUrls: ['./create-post.component.css']
})
export class CreatePostComponent {
  public profile$: Observable<Profile | undefined>;

  constructor(
    public postService: PostsService,
    private profileService: ProfileService
  ) {
    this.profile$ = profileService.profile$;
  }


  onPost(form: NgForm):void{
    
    let postedBy = parseInt(form.value.id ?? "");
    let title = (form.value.title ?? "");
    let content = (form.value.content ?? "");
    let description = (form.value.description ?? "");
    let time = (form.value.dateTime)
    let tag = (form.value.tag ?? "");

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
