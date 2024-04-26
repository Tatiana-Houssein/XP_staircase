import { Component } from '@angular/core';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { StimulusService } from 'src/app/services/stimulus.service';

@Component({
  selector: 'app-form-beginning',
  templateUrl: './form-beginning.component.html',
  styleUrls: ['./form-beginning.component.scss'],
})
export class FormBeginningComponent {
  csps = [
    'agriculteur exploitant',
    "commerçant, artisan ou chef d'entreprise",
    'cadre ou profession intellectuelle supérieure',
    'profession intermédiaire',
    'employé ou ouvrier',
    'étudiant',
    'sans emploi',
  ];

  genres = ['masculin', 'féminin', 'autre', 'je ne veux pas préciser'];

  ageControl = new FormControl('');
  genreControl = new FormControl('');
  cspControl = new FormControl('');
  myForm: FormGroup;

  constructor(
    private router: Router,
    private fb: FormBuilder,
    private stimulusService: StimulusService
  ) {
    this.myForm = this.fb.group({
      age: this.ageControl,
      genre: this.genreControl,
      csp: this.cspControl,
    });
  }

  sendToInfoFirstTask(): void {
    this.stimulusService.sendForm(this.myForm.value);
    this.router.navigate(['/info-first-task']);
  }
}
