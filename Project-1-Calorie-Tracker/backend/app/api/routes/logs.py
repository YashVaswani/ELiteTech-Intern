from datetime import date, datetime, time, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.models import FoodLog, User
from app.db.session import get_db
from app.schemas.log import DailySummary, FoodLogCreate, FoodLogOut
from app.services.nutrition_service import get_nutrition_for_grams

router = APIRouter(prefix="/api/logs", tags=["logs"])


@router.post("", response_model=FoodLogOut, status_code=status.HTTP_201_CREATED)
def create_log(
    payload: FoodLogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> FoodLog:
    try:
        nutrition = get_nutrition_for_grams(payload.food_name, payload.serving_grams)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    log = FoodLog(
        user_id=current_user.id,
        food_name=nutrition.food_name,
        serving_grams=payload.serving_grams,
        calories=nutrition.calories,
        protein_g=nutrition.protein_g,
        carbs_g=nutrition.carbs_g,
        fat_g=nutrition.fat_g,
        confidence=payload.confidence,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.get("", response_model=list[FoodLogOut])
def list_logs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[FoodLog]:
    return (
        db.query(FoodLog)
        .filter(FoodLog.user_id == current_user.id)
        .order_by(FoodLog.logged_at.desc())
        .all()
    )


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_log(
    log_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    log = db.query(FoodLog).filter(FoodLog.id == log_id, FoodLog.user_id == current_user.id).first()
    if log is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log entry not found")
    db.delete(log)
    db.commit()


@router.get("/summary/{on_date}", response_model=DailySummary)
def daily_summary(
    on_date: date,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> DailySummary:
    start = datetime.combine(on_date, time.min, tzinfo=timezone.utc)
    end = datetime.combine(on_date, time.max, tzinfo=timezone.utc)

    entries = (
        db.query(FoodLog)
        .filter(FoodLog.user_id == current_user.id, FoodLog.logged_at.between(start, end))
        .order_by(FoodLog.logged_at.asc())
        .all()
    )

    totals = (
        db.query(
            func.coalesce(func.sum(FoodLog.calories), 0.0),
            func.coalesce(func.sum(FoodLog.protein_g), 0.0),
            func.coalesce(func.sum(FoodLog.carbs_g), 0.0),
            func.coalesce(func.sum(FoodLog.fat_g), 0.0),
        )
        .filter(FoodLog.user_id == current_user.id, FoodLog.logged_at.between(start, end))
        .one()
    )

    total_calories, total_protein, total_carbs, total_fat = totals

    return DailySummary(
        date=on_date.isoformat(),
        total_calories=round(total_calories, 1),
        total_protein_g=round(total_protein, 1),
        total_carbs_g=round(total_carbs, 1),
        total_fat_g=round(total_fat, 1),
        goal_calories=current_user.daily_calorie_goal,
        entries=entries,
    )
