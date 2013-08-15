/**
 * Created with PyCharm.
 * User: alessandro
 * Date: 8/15/13
 * Time: 12:10 PM
 * To change this template use File | Settings | File Templates.
 */
describe("A suite is just a function", function() {
  var a;
  it("and so is a spec", function() {
    a = true;
    expect(a).toBe(true);
  });
});