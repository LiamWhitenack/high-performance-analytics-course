module scrabble_gpu
  use openacc
  implicit none
contains

  subroutine score_many_placements(boards, board_idx, row_idx, col_idx, scores)
    ! boards: (Nboards, R, C)   values 0/1
    ! board_idx,row_idx,col_idx: placement indices, length = M
    ! scores: (M) output
    integer, intent(in) :: boards(:,:,:)
    integer, intent(in) :: board_idx(:), row_idx(:), col_idx(:)
    integer, intent(out) :: scores(:)

    integer :: M, R, C
    integer :: i, b, r, c
    integer :: left, right, up, down, rr, cc

    R = size(boards,2)
    C = size(boards,3)
    M = size(board_idx)

    !$acc data copyin(boards, board_idx, row_idx, col_idx) copyout(scores)
    !$acc parallel loop gang vector present(boards, board_idx, row_idx, col_idx, scores)
    do i = 1, M
       b = board_idx(i)
       r = row_idx(i)
       c = col_idx(i)
       left = 0; right = 0; up = 0; down = 0

       ! count contiguous tiles left/right
       do cc = c-1, 1, -1
          if (boards(b,r,cc) == 1) then
             left = left + 1
          else
             exit
          end if
       end do
       do cc = c+1, C
          if (boards(b,r,cc) == 1) then
             right = right + 1
          else
             exit
          end if
       end do

       ! count contiguous tiles up/down
       do rr = r-1, 1, -1
          if (boards(b,rr,c) == 1) then
             up = up + 1
          else
             exit
          end if
       end do
       do rr = r+1, R
          if (boards(b,rr,c) == 1) then
             down = down + 1
          else
             exit
          end if
       end do

       scores(i) = (left + right + 1) + (up + down + 1) - 1
    end do
    !$acc end data
  end subroutine score_many_placements

end module scrabble_gpu
