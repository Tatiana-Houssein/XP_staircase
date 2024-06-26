import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { NgOptimizedImage } from '@angular/common';
import { ExperimentComponent } from './experiments/experiment/experiment.component';
import { TacheInterferenteComponent } from './forms/tache-interferente/tache-interferente.component';
import { StoreModule } from '@ngrx/store';
import { appReducer } from './@store/reducers';
import { DespairComponent } from './header/despair/despair.component';
import { AppEffects } from './@store/effects';
import { EffectsModule } from '@ngrx/effects';
import { UserInfoComponent } from './forms/user-info/user-info.component';
import { ReactiveFormsModule } from '@angular/forms';
import { InfoSecondTaskComponent } from './forms/info-second-task/info-second-task.component';
import { InfoFirstTaskComponent } from './forms/info-first-task/info-first-task.component';
import { InfoThirdTaskComponent } from './forms/info-third-task/info-third-task.component';
import { FormBeginningComponent } from './forms/form-beginning/form-beginning.component';
import { FormEndingComponent } from './forms/form-ending/form-ending.component';

@NgModule({
  declarations: [
    AppComponent,
    ExperimentComponent,
    TacheInterferenteComponent,
    DespairComponent,
    UserInfoComponent,
    InfoSecondTaskComponent,
    InfoFirstTaskComponent,
    InfoThirdTaskComponent,
    FormBeginningComponent,
    FormEndingComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    NgOptimizedImage,
    StoreModule.forRoot({ app: appReducer }, {}), // 'app' is the key for your reducer
    EffectsModule.forRoot([AppEffects]),
    ReactiveFormsModule,
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
