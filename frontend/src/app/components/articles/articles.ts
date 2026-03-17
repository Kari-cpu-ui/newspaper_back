import { Component, signal } from '@angular/core';
import { ArticulosService, Article } from '../../services/article'; 


@Component({
  selector: 'app-articles',
  standalone: true,
  templateUrl: './articles.html',
  styleUrls: ['./articles.scss']
})
export class ArticlesComponent {
callReview(arg0: number) {
throw new Error('Method not implemented.');
}
callDelete(arg0: number) {
throw new Error('Method not implemented.');
}
callPublish(arg0: number) {
throw new Error('Method not implemented.');
}
  articles = signal<Article[]>([]); // señal tipada con Article

  constructor(private articulosService: ArticulosService) {
    this.articulosService.getArticles().subscribe({
      next: (data: Article[]) => this.articles.set(data),
      error: (err: unknown) => console.error(err)
    });
  }

  deleteArticle(id: number) {
    this.articulosService.deleteArticle(id).subscribe(() => {
      this.articles.set(this.articles().filter(a => a.id !== id));
    });
  }

  publishArticle(id: number) {
    this.articulosService.publishArticle(id).subscribe((updated: Article) => {
      this.articles.set(this.articles().map(a => a.id === id ? updated : a));
    });
  }

  reviewArticle(id: number) {
    this.articulosService.reviewArticle(id).subscribe((updated: Article) => {
      this.articles.set(this.articles().map(a => a.id === id ? updated : a));
    });
  }
}

export { Article };
