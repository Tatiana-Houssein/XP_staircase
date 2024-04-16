import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { StimulusService } from 'src/app/services/stimulus.service';

@Component({
  selector: 'app-form-ending',
  templateUrl: './form-ending.component.html',
  styleUrls: ['./form-ending.component.scss'],
})
export class FormEndingComponent implements OnInit {
  form!: FormGroup;

  constructor(
    private fb: FormBuilder,
    private stimulusService: StimulusService
  ) {}

  ngOnInit(): void {
    this.form = this.fb.group({
      question1: [''], // Yes/No answer
      question2: [''], // three options
      question3: [''], // yes/no answer
    });
  }

  finishExperiment(): void {
    console.log(this.form.value);
    this.stimulusService.sendForm(this.form.value);
    // this.router.navigate(['/info-first-task']);
  }
}
