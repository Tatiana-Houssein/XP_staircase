import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-form-beginning',
  templateUrl: './form-beginning.component.html',
  styleUrls: ['./form-beginning.component.scss'],
})
export class FormBeginningComponent {
  constructor(private router: Router) {}

  sendToInfoFirstTask(): void {
    this.router.navigate(['/info-first-task']);
  }
}
