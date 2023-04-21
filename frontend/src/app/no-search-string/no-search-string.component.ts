import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-no-search-string',
  templateUrl: './no-search-string.component.html',
  styleUrls: ['./no-search-string.component.css']
})
export class NoSearchStringComponent {
  constructor(
    private dialogRef: MatDialogRef<NoSearchStringComponent>) {}

  close(): void {
    this.dialogRef.close();
  }
}
