The image will be drawn at a fractional pixel position on the layer canvas, so some blurring is to be expected unless interpolation is disabled (which would have the same effect as offsetting the drawn image to an integer pixel position - pixel perfect but in slightly wrong position).
I understand that, but why don't create a WMS query do not have fractional pixel (I hope that a pull request will be accepted :-) )
I think it is the calculation of the size that is at fault, it should be an integer value greater than the view size on both sides

e.g instead of

    const requestWidth = ceil(
      (this.ratio_ * getWidth(extent)) / imageResolution,
      DECIMALS
    );

use

    let requestWidth = ceil(
      getWidth(extent) / imageResolution,
      DECIMALS
    );
    requestWidth += 2 * ceil(
      ((this.ratio_ - 1) * requestWidth) / 2,
      DECIMALS
    );

and similarly for `requestHeight`.
That would also apply to other subclasses of ImageSource which have a `ratio` option.
Looks good, thanks, I will try with it :-)