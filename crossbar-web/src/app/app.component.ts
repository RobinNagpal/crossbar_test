import {Component} from '@angular/core';
import {AuthService} from "./services/auth.service";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'Crossbar Test App';
  user = {
    'email': 'robinnagpal.tiet@gmail.com',
    'password': 'secret'
  };

  constructor(private authService: AuthService) {
    this.authService = authService;
  }

  onSubmit() {
    this.authService.loginUser(this.user).subscribe(res => this.user = res);
  }
}
