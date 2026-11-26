package com.gdgoc.backend.posting.repository;

import com.gdgoc.backend.posting.entity.Posting;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PostingRepository extends JpaRepository<Posting, Long> {
}