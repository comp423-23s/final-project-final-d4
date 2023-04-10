import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Post, PostsService } from '../post.service';
import { Observable, Subscription } from 'rxjs';
import { ProfileService, Profile } from '../profile/profile.service';
import { HttpErrorResponse } from '@angular/common/http';

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
    let description = (form.value.description ?? "");
    let time = (form.value.dateTime)
    let tag = (form.value.tag ?? "");

    
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
