# backend/eval/omr_eval.py
from typing import Dict, List
from backend.api.schemas import OMRResult, StudentMeta, QuestionBreakdown
import random, base64, json

def evaluate_omr_image(image_bytes: bytes, student_meta: StudentMeta, answer_key: Dict[int,str]=None) -> Dict:
    """
    Demo evaluator.
    - If answer_key provided, this function will still produce a full OMRResult-style dict.
    - For demo we randomly pick answers (deterministic via hash would be better).
    In production replace with real OMR extraction.
    """
    total_questions = 100
    if answer_key is None:
        answer_key = {i+1: random.choice(['a','b','c','d']) for i in range(total_questions)}

    qbreak = []
    correct_count = 0
    for i in range(total_questions):
        qno = i + 1
        sel = random.choice(['a','b','c','d', None])
        is_correct = (sel == answer_key.get(qno))
        if is_correct:
            correct_count += 1
        qbreak.append({"question_no": qno, "selected_option": sel if sel is not None else "", "is_correct": is_correct})

    per_subject_scores = {f"sub_{i+1}": sum(1 for j in range(i*20, (i+1)*20) if qbreak[j]['is_correct']) for i in range(5)}
    total_score = sum(per_subject_scores.values())

    # for audit overlay placeholder
    overlay_b64 = base64.b64encode(b"overlay-placeholder").decode('utf-8')

    omr_result = {
        "student_meta": student_meta.dict() if hasattr(student_meta, "dict") else student_meta,
        "per_subject_scores": per_subject_scores,
        "total_score": total_score,
        "question_breakdown": qbreak,
        "audit": {"overlay_b64": overlay_b64}
    }
    return omr_result
