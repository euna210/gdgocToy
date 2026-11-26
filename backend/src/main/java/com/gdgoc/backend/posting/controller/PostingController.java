package com.gdgoc.backend.posting.controller;

import com.gdgoc.backend.posting.dto.PostingResponse;
import com.gdgoc.backend.posting.service.PostingService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/postings")
@RequiredArgsConstructor
public class PostingController {

    private final PostingService postingService;

    @GetMapping
    public List<PostingResponse> getAllPostings() {
        return postingService.getAllPostings()
                .stream()
                .map(PostingResponse::from)
                .toList();
    }

    @GetMapping("/{id}")
    public ResponseEntity<PostingResponse> getPosting(
            @PathVariable("id") Long id) {

        return postingService.getPosting(id)
                .map(PostingResponse::from)
                .map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }
}