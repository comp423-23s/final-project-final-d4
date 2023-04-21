import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { Router } from '@angular/router';

@Component({
  selector: 'app-no-search-result',
  templateUrl: './no-search-result.component.html',
  styleUrls: ['./no-search-result.component.css']
})
export class NoSearchResultComponent {
  constructor(
    private dialogRef: MatDialogRef<NoSearchResultComponent>,
    private router: Router) {}

  close(): void {
    this.dialogRef.close();
  }
}
