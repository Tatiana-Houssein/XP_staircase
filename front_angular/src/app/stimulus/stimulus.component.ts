import { ImageService } from './../image.service';
import { StimulusService } from './../stimulus.service';
import { Component, OnInit } from '@angular/core';
import { Stimulus } from '../stimulus.model';
import { delay, timer } from 'rxjs';

@Component({
  selector: 'app-stimulus',
  templateUrl: './stimulus.component.html',
  styleUrls: ['./stimulus.component.scss']
})
export class StimulusComponent implements OnInit{
  stimulus!: Stimulus;
  cheminRacine: string = "assets/tokens";
  cheminImage: string = `${this.cheminRacine}/token_0.png`;
  isButtonsDisabled: boolean = false;

  constructor(
    private stimulusService: StimulusService,
    private imageService: ImageService,
  ) {}


  ngOnInit(): void {
    console.log("EEEEEEEEEEEEEEEEEEEEEEE");
    this.stimulusService.getFirstStimulus().subscribe(
      data => {
        this.disableButtons()
        console.log(data);
        this.stimulus = data;
        this.preloadImage(this.stimulus.id);
        this.preloadImage(this.stimulus.nextId);
        this.cheminImage = `${this.cheminRacine}/token_${this.stimulus.id}.png`;
        console.log(this.cheminImage);
      },
      error => {
        // Handle errors
        console.error(error);
      },
      () => {
        console.log("reEnabling");
        this.enableButtons();
      },
    );
  }

  preloadImage(id: number): void {
    const img = new Image();
    this.imageService.getImage(id).subscribe(
      imageUrl => {
        img.src = imageUrl;
      }
    );
  }

  disableButtons(): void {
    this.isButtonsDisabled = true;
  }

  enableButtons(): void {
    timer(2000).subscribe(
      () => {
        this.isButtonsDisabled = false;
      }
    );
  }


  dejaVu(): void {
    this.disableButtons();
    this.cheminImage = `${this.cheminRacine}/token_0.png`;
    this.stimulusService.sendSubjectAnswer(true).subscribe
    (
      data => {
        console.log("DV: disabling");
        console.log(data);
        this.stimulus = data;
        this.preloadImage(this.stimulus.id);
        this.preloadImage(this.stimulus.nextId);
        timer(1000).subscribe(
          () => {
            this.cheminImage = `${this.cheminRacine}/token_${this.stimulus.id}.png`;
          }
        );
        console.log(this.cheminImage);
      },
      error => {
        // Handle errors
        console.error(error);
      },
      () => {
        console.log("reEnabling");
        this.enableButtons();
      },
    );
  }

  jamaisVu(): void {
    this.disableButtons();
    this.cheminImage = `${this.cheminRacine}/token_0.png`;
    this.stimulusService.sendSubjectAnswer(false).subscribe(
      data => {
        console.log(data);
        this.stimulus = data;
        this.preloadImage(this.stimulus.id);
        this.preloadImage(this.stimulus.nextId);
        timer(1000).subscribe(
          () => {
            this.cheminImage = `${this.cheminRacine}/token_${this.stimulus.id}.png`;
          }
        );
        console.log(this.cheminImage);
      },
      error => {
        // Handle errors
        console.error(error);
      },
      () => {
        console.log("reEnabling");
        this.enableButtons();
      },
    );
  }

}
