import { Component, OnInit } from '@angular/core';
import { ServiceManagerService } from '../service-manager.service';

@Component({
  selector: 'app-ott-blogs',
  templateUrl: './ott-blogs.component.html',
  styleUrls: ['./ott-blogs.component.scss']
})
export class OttBlogsComponent implements OnInit {

  constructor(
    private serviceManager: ServiceManagerService) { }

  blogs: Blog[] = []

  ngOnInit(): void {
    // Blogs
    this.serviceManager.getBlogs().subscribe(data => {
      this.blogs = data.blogs;
      console.log("Live Blogs : ", this.blogs);
    });
  }

  blogsSlideConfig = {
    "slidesToShow": 3.5,
    "slidesToScroll": 1,
    "dots": false,
    "infinite": false
  };

  slickInit(e: any) {
    console.log('slick initialized');
  }

  breakpoint(e: any) {
    console.log('breakpoint');
  }

  afterChange(e: any) {
    console.log('afterChange');
  }

  beforeChange(e: any) {
    console.log('beforeChange');
  }

}

interface Blog {
  id: number,
  title: string,
  description: string,
  image: string,
  date: string
}