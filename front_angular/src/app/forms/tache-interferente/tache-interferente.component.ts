// second-page.component.ts

import { Component, ElementRef, OnInit, Renderer2 } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { Store } from '@ngrx/store';
import { AppState, selectQuestionInterferente } from 'src/app/@store/app.state';

@Component({
  selector: 'app-tache-interferente',
  templateUrl: './tache-interferente.component.html',
  styleUrls: ['./tache-interferente.component.scss'],
})
export class TacheInterferenteComponent implements OnInit {
  questionForm: FormGroup;
  questionInterferente!: string;

  constructor(
    private router: Router,
    private fb: FormBuilder,
    private store: Store<AppState>,
    private renderer: Renderer2,
    private elementRef: ElementRef
  ) {
    this.questionForm = this.fb.group({
      answer: ['', [Validators.required, this.isIntegerValidator]],
    });
    this.store
      .select(selectQuestionInterferente)
      .subscribe((questionInterferente) => {
        this.questionInterferente = questionInterferente;
      });
  }

  ngOnInit(): void {
    this.setFocus();
  }

  setFocus() {
    this.renderer
      .selectRootElement(this.elementRef.nativeElement.querySelector('input'))
      .focus();
  }

  isIntegerValidator(control: any) {
    return Number.isInteger(Number(control.value))
      ? null
      : { notAnInteger: true };
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
