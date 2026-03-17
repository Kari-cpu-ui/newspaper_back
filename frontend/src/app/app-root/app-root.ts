import { Component } from '@angular/core';
import { ArticlesComponent } from '../components/articles/articles';
import { UsersComponent } from '../components/users/users'; 

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ArticlesComponent, UsersComponent],
  templateUrl: './app-root.html',
  styleUrl: './app-root.scss',
})
export class AppRootComponent {

}
