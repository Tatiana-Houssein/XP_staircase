// second-page.component.ts

import { Component, ElementRef, OnInit, Renderer2 } from '@angular/core';
import {
  AbstractControl,
  FormBuilder,
  FormGroup,
  ValidatorFn,
  Validators,
} from '@angular/forms';
import { Router } from '@angular/router';
import { Store } from '@ngrx/store';
import {
  AppState,
  selectQuestionInterferente,
  selectResultTacheInterferente,
} from 'src/app/@store/app.state';

@Component({
  selector: 'app-tache-interferente',
  templateUrl: './tache-interferente.component.html',
  styleUrls: ['./tache-interferente.component.scss'],
})
export class TacheInterferenteComponent implements OnInit {
  questionForm: FormGroup;
  questionInterferente!: string;
  expectedResult!: number;
  wrongAnswer: boolean = false;

  constructor(
    private router: Router,
    private fb: FormBuilder,
    private store: Store<AppState>,
    private renderer: Renderer2,
    private elementRef: ElementRef
  ) {
    this.questionForm = this.fb.group({
      answer: ['', [Validators.required]],
    });
    this.store
      .select(selectQuestionInterferente)
      .subscribe((questionInterferente) => {
        this.questionInterferente = questionInterferente;
      });
    this.store
      .select(selectResultTacheInterferente)
      .subscribe((resultInterferente) => {
        this.expectedResult = resultInterferente;
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

  // isIntegerValidator(control: any) {
  //   if (Number(control.value) === this.expectedResult) {
  //     return null;
  //   } else {
  //     return { notAnInteger: true };
  //   }
  // }

  // isExpectedResultValidator(control: any) {
  //   return Number(control.value) === this.expectedResult
  //     ? null
  //     : { notAnInteger: true };
  // }

  submitForm() {
    console.log(this.questionForm);
    console.log(typeof this.questionForm.value.answer);
    console.log(
      'DADA',
      this.questionForm.value.answer + ' ' + this.expectedResult
    );
    // Handle form submission
    if (Number(this.questionForm.value.answer) === this.expectedResult) {
      // Form is valid, proceed with form submission
      console.log('Form submitted successfully!');
      this.goBackExperiment();
    } else {
      // Form is invalid, display error messages or handle accordingly
      console.error("Ce n' est pas le bon résultat !");
      setTimeout(() => {
        this.wrongAnswer = true;
        console.log('Flag is now false');

        // Set flag back to true after 1 second
        setTimeout(() => {
          this.wrongAnswer = false;
          console.log('Flag is now true');
        }, 2000); // 1000 milliseconds = 1 second
      }, 0); // 1000 milliseconds = 1 second
    }
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
