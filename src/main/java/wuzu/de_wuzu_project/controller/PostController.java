package wuzu.de_wuzu_project.controller;


import org.springframework.web.bind.annotation.*;
import wuzu.de_wuzu_project.domain.Post;
import wuzu.de_wuzu_project.service.PostService;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;

@RestController
@RequestMapping("/posts")
public class PostController {

    private final PostService postService;

    public PostController(PostService postService) {
        this.postService = postService;
    }

    @GetMapping("/today")
    public List<Post> getTodayPosts() {
        boolean isMorning = LocalTime.now().isBefore(LocalTime.NOON);
        return postService.getTodayPostsByTime(isMorning);
    }

//    @GetMapping("/{date}") 이거는 date 로 넣어도 오전 오후 로 볼 수 있게하는
//    public List<Post> getPostsByDate(@PathVariable("date") String date) {
//        LocalDate localDate = LocalDate.parse(date);
//        return postService.getPostsByDateAndTime(localDate, true);
//    }
    @GetMapping("/all")
    public List<Post> getAllPosts() {
        return postService.getAllPostsWithKeywords();
    }
    @PostMapping("/add")
    public Post addPost(@RequestBody Post post) {
        if (post.getDate() == null) {
            post.setDate(LocalDate.now()); // 현재 날짜로 기본값 설정
        }
        if (post.getTime() == null) {
            post.setTime(LocalTime.now()); // 현재 시간으로 기본값 설정
        }
        return postService.savePost(post);
    }
    // 특정 날짜의 모든 데이터를 조회
    @GetMapping("/{date}")
    public List<Post> getPostsByDate(@PathVariable("date")String date) {
        LocalDate localDate = LocalDate.parse(date);
        return postService.getPostsByDate(localDate); // 특정 날짜의 모든 데이터 조회
    }
}
