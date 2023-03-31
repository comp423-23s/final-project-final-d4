import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';

@Component({
  selector: 'app-create-post',
  templateUrl: './create-post.component.html',
  styleUrls: ['./create-post.component.css']
})
export class CreatePostComponent {

  form = this.formBuilder.group({
    id: '',
    title: '',
    description: '',
    details: '',
    comments: ''
  });

  constructor(
    private formBuilder: FormBuilder,
  ) {}

  onSubmit(){
    const newuser = {
      id:this.form.value.id ?? " ",
      title: this.form.value.title ?? " ",
      description: this.form.value.description ?? " ",
      details: this.form.value.details ?? " ",
      comments: this.form.value.comments ?? " "
    };
    this.form.reset();
  }

}
