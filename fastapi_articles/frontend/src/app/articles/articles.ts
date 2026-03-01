import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ArticleService, Article } from '../services/article';

@Component({
  selector: 'app-articles',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './articles.html',
  styleUrl: './articles.css'
})
export class ArticlesComponent implements OnInit {

  articles: Article[] = [];

  newArticle: Article = {
    id: 0,
    nom: '',
    description: '',
    prix: 0,
    en_stock: true
  };

  constructor(private articleService: ArticleService) {}

  ngOnInit(): void {
    this.loadArticles();
  }

  loadArticles() {
    this.articleService.getArticles().subscribe(data => {
      this.articles = data;
    });
  }

  addArticle() {
    this.articleService.addArticle(this.newArticle).subscribe(() => {
      this.loadArticles();
      this.newArticle = {
        id: 0,
        nom: '',
        description: '',
        prix: 0,
        en_stock: true
      };
    });
  }

  deleteArticle(id: number) {
    this.articleService.deleteArticle(id).subscribe(() => {
      this.loadArticles();
    });
  }
}