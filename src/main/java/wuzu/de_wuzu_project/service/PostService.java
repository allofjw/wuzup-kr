package wuzu.de_wuzu_project.service;


import org.springframework.stereotype.Service;
import wuzu.de_wuzu_project.domain.Post;
import wuzu.de_wuzu_project.repository.PostRepository;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;

@Service
public class PostService {
    private final PostRepository postRepository;

    public PostService(PostRepository postRepository) {
        this.postRepository = postRepository;
    }

    public List<Post> getTodayPostsByTime(boolean isMorning) {
        LocalDate today = LocalDate.now();
        LocalTime noon = LocalTime.NOON;

        if (isMorning) {
            return postRepository.findMorningPostsByDate(today, noon);
        } else {
            return postRepository.findAfternoonPostsByDate(today, noon);
        }
    }

    public List<Post> getPostsByDateAndTime(LocalDate date, boolean isMorning) {
        LocalTime noon = LocalTime.NOON;

        if (isMorning) {
            return postRepository.findMorningPostsByDate(date, noon);
        } else {
            return postRepository.findAfternoonPostsByDate(date, noon);
        }
    }
    public List<Post> getAllPosts(){
        return postRepository.findAll();
    }
    public List<Post> getAllPostsWithKeywords() {
        return postRepository.findAllWithKeywords();
    }
    public Post savePost(Post post) {
        return postRepository.save(post);
    }
    // 특정 날짜의 모든 데이터를 조회
    public List<Post> getPostsByDate(LocalDate date) {
        return postRepository.findByDate(date); // 해당 날짜의 모든 데이터 조회
    }

}
