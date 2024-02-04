// second-page.component.ts

import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-tache-interferente',
  templateUrl: './tache-interferente.component.html',
  styleUrls: ['./tache-interferente.component.scss']
})
export class TacheInterferenteComponent {
  questionForm: FormGroup;

  constructor(private router: Router, private fb: FormBuilder) {
    this.questionForm = this.fb.group({
      answer: ['', [Validators.required, this.isIntegerValidator]]
    })
  }

  isIntegerValidator(control: any) {
    return Number.isInteger(Number(control.value)) ? null : {notAnInteger : true};
  }

  submitForm() {
    // Handle form submission
    console.log('Form submitted:', this.questionForm.value);
    this.goBackExperiment();
  }

  onEnter() {
    // Function to be called when Enter is pressed
    console.log('Enter pressed');
  }

  onBlur() {
    // Function to be called when the input field loses focus
    console.log('Input field blurred');

  }

  goBackExperiment(): void {
    this.router.navigate(['/experiment']);
  }
}
