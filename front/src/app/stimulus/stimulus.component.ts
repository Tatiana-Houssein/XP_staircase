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

  constructor(private stimulusService: StimulusService) {}


  ngOnInit(): void {
    this.stimulusService.getTestToken().subscribe(data => {
      console.log(data);
      this.stimulus = data;
    })
  }
}
