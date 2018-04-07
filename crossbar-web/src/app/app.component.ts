import {Component} from '@angular/core';
import {AuthService} from "./services/auth.service";

export interface User {
  id: string;
  email: string;
  password: string;
  token: string;
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'Crossbar Test App';
  user: User = {
    id: null,
    email: "robinnagpal.tiet@gmail.com",
    password: "secret",
    token: null
  };

  constructor(private authService: AuthService) {
    this.authService = authService;
  }

  onLogin() {
    this.authService.loginUser(this.user).subscribe((res: User) => this.user = res);
  }

  connectToWamp() {
    this.authService.loginUser(this.user).subscribe((res: User) => this.user = res);
  }
}
