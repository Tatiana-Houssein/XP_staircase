import { StimulusService } from './../stimulus.service';
import { Component, OnInit } from '@angular/core';
import { Stimulus } from '../stimulus.model';

@Component({
  selector: 'app-stimulus',
  templateUrl: './stimulus.component.html',
  styleUrls: ['./stimulus.component.scss']
})
export class StimulusComponent implements OnInit{
  stimulus!: Stimulus;
  cheminImage!: string;
  cheminRacine: string = "assets/tokens"

  constructor(private stimulusService: StimulusService) {}


  ngOnInit(): void {
    this.stimulusService.getFirstStimulus().subscribe(data => {
      console.log(data);
      this.stimulus = data;
      this.cheminImage = `${this.cheminRacine}/token_${this.stimulus.id}.png`;
      console.log(this.cheminImage);
    })


  }


  dejaVu(): void {
    this.stimulusService.sendSubjectAnswer(true).subscribe(data => {
      console.log(data);
      this.stimulus = data;
      this.cheminImage = `${this.cheminRacine}/token_${this.stimulus.id}.png`;
      console.log(this.cheminImage);
    })
    this.cheminImage = `${this.cheminRacine}/token_${this.stimulus.id}.png`
  }

  jamaisVu(): void {
    this.stimulusService.sendSubjectAnswer(false).subscribe(data => {
      console.log(data);
      this.stimulus = data;
      this.cheminImage = `${this.cheminRacine}/token_${this.stimulus.id}.png`;
      console.log(this.cheminImage);
    })
    this.cheminImage = `${this.cheminRacine}/token_${this.stimulus.id}.png`
  }

}
