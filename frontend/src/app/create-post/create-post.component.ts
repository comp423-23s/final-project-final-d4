import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { PostsService } from '../post.service';

@Component({
  selector: 'app-create-post',
  templateUrl: './create-post.component.html',
  styleUrls: ['./create-post.component.css']
})
export class CreatePostComponent {

  constructor(
    public postService: PostsService
  ) {}

  ngOnInit(): void{

  }

  onPost(form: NgForm){
    if(form.invalid){
      return
    }
    this.postService.addPost(form.value.id, form.value.title, form.value.descripiton, form.value.content, form.value.dateTime, form.value.tag);
    form.resetForm()
  }

}
