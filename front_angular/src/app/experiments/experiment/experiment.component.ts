import { Component, NgZone, OnInit } from '@angular/core';
import { ImageService } from '../../services/image.service';
import { ImagePreloadService } from '../../services/image-preload.service';
import { Router } from '@angular/router';
import { Store } from '@ngrx/store';
import {
  AppState,
  selectCurrentId,
  selectFlagIA,
  selectIsExperimentLaunched,
  selectNextId,
  selectStateMetaExperiment,
} from '../../@store/app.state';
import {
  loadExperimentComponent,
  userRespondToStimulus,
  startNewExperiment,
} from '../../@store/actions';
import { increment } from '../../@store/actions';

@Component({
  selector: 'app-experiment',
  templateUrl: './experiment.component.html',
  styleUrls: ['./experiment.component.scss'],
})
export class ExperimentComponent implements OnInit {
  stateMetaExperiment!: string;
  isExperimentLaunched!: boolean;
  currentImageId!: number;
  nextImageId!: number;
  currentImageUrl!: string;
  nextImageUrl!: string;
  flagIA!: string;
  imageOpacity = 1; // Initial opacity
  buttonsDisabled = false; // Initial state

  constructor(
    private imageService: ImageService,
    private imagePreloadService: ImagePreloadService,
    private router: Router,
    private ngZone: NgZone,
    private store: Store<AppState>
  ) {}

  ngOnInit(): void {
    this.store
      .select(selectIsExperimentLaunched)
      .subscribe((isExperimentLanched) => {
        this.isExperimentLaunched = isExperimentLanched;
      });
    this.store.dispatch(loadExperimentComponent());
    this.store.select(selectCurrentId).subscribe((currentId) => {
      (this.currentImageId = currentId),
        (this.currentImageUrl = this.imageService.getImageUrl(currentId));
    });
    this.store.select(selectNextId).subscribe((nextId) => {
      (this.nextImageId = nextId),
        (this.nextImageUrl = this.imageService.getImageUrl(nextId));
    });
    this.store.select(selectFlagIA).subscribe((flagIA) => {
      this.flagIA = flagIA;
    });
    this.store
      .select(selectStateMetaExperiment)
      .subscribe((stateMetaExperiment) => {
        this.stateMetaExperiment = stateMetaExperiment;
      });
    this.preloadNextImage();
    this.displayImageForLimitedTime(1000);
  }

  sendUserAnswerToBack(chosenNumber: number) {
    this.store.dispatch(
      userRespondToStimulus({ responseToStimulus: chosenNumber })
    );
  }

  preloadNextImage(): void {
    this.imagePreloadService.preloadImage(this.nextImageUrl).subscribe(
      () => {
        // Image is preloaded, you can now update the UI or trigger the change.
        console.log(`Image ${this.nextImageId} preloaded.`);
      },
      (error) => {
        console.error(`Error preloading image ${this.nextImageId}:`, error);
      }
    );
  }

  userClickButton(chosenNumber: number) {
    this.sendUserAnswerToBack(chosenNumber);
    if (this.nextImageId === -1) {
      this.router.navigate(['/info-second-task']);
    } else {
      this.router.navigate(['/calcul-mental']);
    }
  }

  private displayImageForLimitedTime(timeDisplay: number): void {
    // Set opacity to 1 for display
    this.imageOpacity = 1;
    this.buttonsDisabled = true;

    // After 1 second, reset the opacity
    setTimeout(() => {
      // Ensure that Angular change detection is triggered within NgZone
      this.ngZone.run(() => {
        this.imageOpacity = 0;
        this.buttonsDisabled = false;
      });
    }, timeDisplay);
  }
}
