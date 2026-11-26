package com.gdgoc.backend.posting.service;

import com.gdgoc.backend.posting.entity.Posting;
import com.gdgoc.backend.posting.repository.PostingRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class PostingService {

    private final PostingRepository postingRepository;

    public List<Posting> getAllPostings() {
        return postingRepository.findAll();
    }

    public Optional<Posting> getPosting(Long id) {
        return postingRepository.findById(id);
    }
}